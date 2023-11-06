# fff-mock-gen

fff-mock-gen automatically scans your header files and generates all the mocks for the FFF library (https://github.com/meekrosoft/fff)

## Quickstart

Install Library: 

```
pip install fff-mock-gen
```

Run:

```
fff-mock-gen -i '/PATH/TO/HEADERS' -o '/OUTPUT/DIRECTORY'
```

### Limitations

Public function prototypes cannot contain any array lengths. For example/

```
uint32_t public_function(float input[3])
```

Must be declared as:

```
uint32_t public_function(float* input)
```




