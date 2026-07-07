# Hint — 01_env_vars

1. In Python: `import os` and `os.environ.get("APP_NAME")`
2. `get` returns `None` if the key does not exist — handle that case
3. In C++: `#include <cstdlib>` and `std::getenv("APP_NAME")`
4. `getenv` returns `nullptr` if absent
