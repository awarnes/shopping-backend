# Shopping List Backend

"Simple" backend with SQLite database for the [shopping-frontend](https://github.com/awarnes/shopping-frontend) project.

### Basic setup

```bash
pipenv install
./bootstrap.sh
```

Check out the `/docs` folder for information on using the API

### Todos
- Get product details from integrators (by product.sku)
- Update responses to include fully realized objects (e.g., return `User.products` as array of `Product` objects rather than just database IDs)
- Upgrade to make use of PostgreSQL database instead of SQLite