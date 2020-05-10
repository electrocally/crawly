# Crawly
A quick and dirty script to find content inside a folder (and inside a folder (and inside a folder))

***Disclaimer: This is a work in progress and by no means do I accept any responsibility or liability if you wreck your shit/anything with it.***

## Usage

Crawly is built using click, so its pretty descriptive for different options
```python
$ python3 crawly.py --help
```

A couple options:

### Simple search 
```python
$ python3 crawly.py thing
```

### Case Sensitive search 
```python
$ python3 crawly.py Thing --case
```

### Regex search 
```python
$ python3 crawly.py '^Thing$' --regex
```

