# Command Line Crypto

This is a simple implementation of the ciphers from "Hacking Secret Ciphers with Python" by Al Sweigart. A PDF of the book is floating around on the internet somewhere; I remember it being easy to find. **Thanks, Al!**

Note: these are not secure methods of encryption, just some fooling around.

## Usage

`$ python setup.py install`

`$ crypto -e "text to be encyphered" -v "vigenerekey"

`$ crypto -d "text to be decyphered" -v "vigenerekey"

Other ciphers are implemented, check out the code. Their usage is similar, I'm just in a rush to document.

Also, note that some ciphers (esp. obfuscation) might be destructive when used with others! Be careful with this.