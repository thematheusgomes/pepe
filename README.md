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
```

# Tasks

## WAF IP release

IP should be on CIDR notation. Example event:
```
    {
        "action": "allow",
        "location": ( "mx" || "br" || "us" || "song" || "mariano" || "john" || "andres" ),
        "ip": "0.0.0.0/32" 
    }

```

WAF Global: 

`aws waf list-ip-sets --query "IPSets[*]" | jq '.[] | "\(.Name) \(.IPSetId)"'`

WAF Regional: 

`aws waf-regional list-ip-sets --query "IPSets[*]" --region us-east-1 | jq '.[] | "\(.Name) \(.IPSetId)"'`

