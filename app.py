from flask import Flask, request, jsonify, render_template
import grpc
from lnd_connection import connection_lnd,connection_lnd_invoices,lightning_pb2 as ln,invoicesrpc 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invoice', methods=['POST'])
def create_invoice():
    amount_sat = request.json.get('amount')
    
    if not amount_sat:
        return jsonify({'error': 'Amount is required'}), 400

    try:
        # Convierte amount_sat a entero
        amount_sat = int(amount_sat)
    except ValueError:
        return jsonify({'error': 'Amount must be an integer'}), 400


    invoice_req = ln.Invoice(
        value=amount_sat,
        memo="Tip"
    )

    conn_lnd = connection_lnd("invoice")

    try:
        invoice = conn_lnd.AddInvoice(invoice_req)    
        r_hash_hex = invoice.r_hash.hex()
        return jsonify({
            'payment_request': invoice.payment_request,
            'r_hash': r_hash_hex
        })
    except grpc.RpcError as e:
     return jsonify({'error': str(e)}), 500     

            
@app.route('/check_payment/<r_hash>', methods=['GET'])
def check_payment(r_hash):    

    try:
        r_hash_bytes = bytes.fromhex(r_hash)
    except ValueError:
        return jsonify({'error': 'Invalid r_hash format'}), 400

    conn_lnd =connection_lnd_invoices()

    try:
        
        request = invoicesrpc.LookupInvoiceMsg(payment_hash=r_hash_bytes)
        invoice = conn_lnd.LookupInvoiceV2(request)        
                
        if invoice.state == 1:
            return jsonify({'settled': True, 'state': 'PAID'})
        elif invoice.state == 0:
            return jsonify({'settled': False, 'state': 'PENDING'})
        elif invoice.state == 2:
            return jsonify({'settled': False, 'state': 'CANCELED'})
        elif invoice.state == 3:        
            return jsonify({'settled': False, 'state': 'ACCEPTED'})
        else:
            return jsonify({'settled': False, 'state': 'UNKNOWN'})
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
