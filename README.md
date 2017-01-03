# My git template

This is my git template. The only things that are changed are the hooks. I use python.

## How to use

Download this packages wherever you want, say in `~/git-template`

```bash
git config --global --set init.templateDir "~/git-template/content"
```


### CSW - Check Stdout Writers

This hook (`.git/hooks/py/check-stdout-writers.py`) checks that you haven't left a `print` in your python files, a `console.log` in your js, etc.

#### Escaping

You can escape an SW by making sure there is, in the line just above, this: `CSW: ignore`

```js
if (language == 'js') {
    language = 'javascript'
}
// CSW: ignore
console.log('I dont block your commit')

console[log]('me either!')

console.log('But I do')
```

If you want to escape the entire file, make sure that in the *first* or *second* line, there is this: `CSW: ignore *`

```python
# CSW: ignore *

print('not blocking')

print('me either')

print('great!')
```
