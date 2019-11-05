Generates XKCD passwords. See https://xkcd.com/936/

No logs.

Custom password masks available.
- `%d` for digit
- `%p` for special character
- `%w` for lowercased word
- `%W` for Capitalized word
- `%C` for UPPERCASED word

Example:  
`%w-%w-%w-%w` outputs `escalators-better-vaccinate-nonabsorbent`  
`%w-%W-%C%s%d%d%d` outputs `carousels-Foreshadowing-DISHWATER@934`
