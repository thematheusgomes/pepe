# Set up

##### Clone Repository

```
git clone git@github.com:thematheusgomes/pepe.git
```

### Environment

Requirements:

Install the packages below:
- python3.9
- node 14
- yarn
- pipenv

Refresh aws tokens using [aws-google-auth](https://github.com/Boomcredit/boomcredit-devops/wiki/Sign-in-to-AWS-using-GSuite-credentials)

Install serverless packages:
```
yarn install
```

Start a virtualenv:
```
pipenv shell
```

Install all python dependencies:
```
pipenv install
```
An alternative is to use the functions from the `/tools/scripts.sh` file:
```bash
source /tools/scripts.sh
```

### Run locally

You can run Pepe locally using the `serverless-offline` and `ngrok` packages.

After installing all prerequisites run the command:
```
serverless offline
```

In addition you can create an HTTPS endpoint using ngrok:
```
ngrok http 3000
```

To configure this endpoint in the development bot, go to the google cloud, select the `Superset` project, then look for the Google Chat service, and click manage, there you will have the option to set the endpoint where the bot should forward the message.

### Deployment

After installing the serverless packages and all python dependencies, you can deploy the environment for dev by running the command:
```
yarn deploy:dev
```

To deploy to the tools environment, run the command:
```
yarn deploy:tools
```

To deploy just the function without changing the infrastructure, run the command:
```
yarn deploy:function:tools
```

If you want to consult the scripts, take a look at the `package.json` file.

# Available Commands

`/iprelease <publicIp>`
`/iprelease <action> <publicIp>`

**supported action:** [dynamic, fixed, clean] (clean remove all dynamic ips)
**supported publicIp:** [IPv4, IPv6]

`/sgipupdate <environment> <publicIp>`

**supported environments:** [dev, qa, tools, prod]
**supported publicIp:** [IPv4, IPv6]

`/turnonoff <action> <environment> <target>`

**supported actions:** [start, stop]
**supported environments:** [dev, qa, tools] (tools is only supported for target bastion)
**supported targets:** [bastion, clusters]
