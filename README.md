# Set up

### Clone Repository

```
git clone git@github.com:Boomcredit/pepe.git
```

### Environment

Refresh aws tokens using [aws-google-auth](https://github.com/Boomcredit/boomcredit-devops/wiki/Sign-in-to-AWS-using-GSuite-credentials)

Get a set of ready to use functions (bash):
```bash
cd pepe/
source scripts.sh
py-env
```

### Deployment

After you install all python required modules, run:
```
npm run deploy:dev
```

# Available Commands

- `/iprelease`
    - `/iprelease <publicIp>` (Add your ip to the dynamic ips list)
    - `/iprelease dynamic <publicIp>` (Another option that add your ip to the dynamic ips list)
    - `/iprelease fixed <publicIp>` (Add your ip to the fixed ips list)
    - `/iprelease clean` (Remove all ips from dynamic ips list)

- `/sgipupdate`
    - `/sgipupdate dev <publicIp>` (Update IP in the Dev Security Group)
    - `/sgipupdate qa <publicIp>` (Update IP in the Qa Security Group)
    - `/sgipupdate prod <publicIp>` (Update IP in the Prod Security Group)
    - `/sgipupdate tools <publicIp>` (Update IP in the Tools Security Group)
