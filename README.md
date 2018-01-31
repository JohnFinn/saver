The following script will take > 10 seconds to execute each time you run program
but it is annoying to wait every time you run it when you are not finished developing
```python
def foo(number):
  import time
  time.sleep(5)
  return number

foo(10)
foo(20)
```
so here is the solution
```python
from saver import saver

@saver('filename')
def foo(number):
  ...
```
this function will execute only if it wasn't executed before with same argument
or, it's source was changed
result will be saved in file, and fetched next time you call function

after compliting development simply remove 'from saver import saver', '@saver("filename")' and file "filename"
