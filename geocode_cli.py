"""Usage: geocode_cli.py [-h] ADDRESS

Accepts the <address> and attempts to geocode it.

Arguments: 
    address     A comma delimited address, letters, numbers delimited by commas.
                Allowed special charachters (),./-

Options:
    -h  --help

"""
from docopt import docopt
from geocoder import geocoder
from validator import validate_address

def main():
    args = docopt(__doc__)
    address =args["ADDRESS"]
    if validate_address(address):
        address_match = geocoder.Address(address)
        try:
            # TODO This API needs cleaning up. There is too much of the geocoder 
            # logic exposed here.
            address_match.geocode()
            print(address_match.coords)
        except geocoder.AddressNotMatched:
            print("The addres could not be found")
    else:
        print("Invalid Address")

if __name__ == "__main__":
    main()
