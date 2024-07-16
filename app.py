from flask import Flask, request, jsonify, render_template
import grpc
from lnd_connection import connection_lnd,ln


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/invoice', methods=['POST'])
def create_invoice():
    amount_sat = request.json.get('amount')
    print(amount_sat)
    #memo = request.json.get('memo', 'Tip')
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

            

if __name__ == '__main__':
    app.run(debug=True)
