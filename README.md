## 🛍️ Buy, Sell, and Pawn API with FastAPI

### API Explanation:
The Buy, Sell, and Pawn API is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI provides automatic generation of interactive API documentation (using Swagger UI and ReDoc), increased development speed, and easy integration with modern frontend frameworks.

### API Features:
- **Sell Items**: 💰 Users can list items they no longer need for sale by making POST requests to the `/sell` endpoint. They provide item details such as description, images, and price. Both users and businesses can contraoffer on prices by sending PATCH requests to update the listing.

- **Buy Items**: 🛒 Buyers can search for items they are interested in purchasing by making GET requests to the `/buy` endpoint. They can view listings provided by sellers, filter results based on their preferences, and make purchases directly through the platform. Both users and businesses can contraoffer on prices by sending PATCH requests to negotiate with sellers.

- **Pawn Items**: 🏦 Users can pawn items for a short-term loan by making POST requests to the `/pawn` endpoint. They provide item details as collateral and receive cash in return. Both users and businesses can contraoffer on loan terms by sending PATCH requests to update the pawn agreement.
