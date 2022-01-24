# GetScoped
Extracting In and Out-of-Scope hosts from dnsx output

## Usage

```
usage: getscoped.py [-h] -s SCOPE -d DNSX [-oI OUTPUT_IN] [-oO OUTPUT_OUT]

optional arguments:
  -h, --help            show this help message and exit
  -s SCOPE, --scope SCOPE
                        Scope file containing CIDRs and/or IP addresses
  -d DNSX, --dnsx DNSX  JSON output file from dnsx
  -oI OUTPUT_IN, --output-in OUTPUT_IN
                        Output for in-scope hosts (default='in-scope.txt')
  -oO OUTPUT_OUT, --output-out OUTPUT_OUT
                        Output for out-of-scope hosts (default='out-of-scope.txt')
```

## Example

```
python3 -s scope.txt -d dnsx.output.json -oI in-scope-hosts.txt -oO out-of-scope-hosts.txt
```