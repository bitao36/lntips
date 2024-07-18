# lntips
Simple lightning app to receive tips

## Requirements

- Python 3.10 or higher
- Python dependencies `Flask`,`decouple`,`grpcio`,`protobuf`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/bitao36/lntips.git
cd lntips
```

2. Create a virtual environment and activate it:

**For Linux:**

install these dependencies to crate virtual environment
```
sudo apt-get install python3-dev
```

Install virtual environment just the first time

```bash
python3 -m venv venv
```

Activate the virtual environment (activate the environment every time you go to run the endpoint)


```bash
source venv/bin/activate
```

**For Windows:**


Install virtual environment just the first time


```bash
virtualenv venv
```

Activate the virtual environment (activate the environment every time you go to run the endpoint)

```bash
venv\Scripts\.\activate
```


3. Install the required dependencies:

```bash
pip install -r requirements.txt
```


### Environment Variables

To test the project i suggest that you use [Polar](https://lightningpolar.com/) tool to create a lightning network with two LND nodes.
Then you select one node and  must copy files tls.cert,invoices.macaroon y admin.macaroon to credentials folder.

![info_connect_node](https://hackmd.io/_uploads/B12EJ1AyC.png)

You must create a file .env and to add the following environment variables to customize the connection to the LND node selected:

```bash=
LND_RPC_ADDRESS=127.0.0.1:port
LND_TLS_CERT_PATH=credentials/tls.cert
LND_INVOICE_MACAROON_PATH=credentials/invoices.macaroon
LND_ADMIN_MACAROON_PATH=credentials/admin.macaroon
```


## Access the application

### Server execution

```
flask run
```

### Web client

Go to browser 
```
http://localhost:5000
```