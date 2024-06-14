import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const client = createClient();

const asynGet = promisify(client.get).bind(client);
const asynSet = promisify(client.set).bind(client);

const listProducts = [
  { Id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { Id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { Id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { Id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find((product) => product.Id === id);
}

async function reserveStockById(itemId, stock) {
  await asynSet(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  return parseInt(await asynGet(itemId));
}

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const currReservedStock =
    (await getCurrentReservedStockById(itemId)) ?? product.stock;

  if (currReservedStock <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, currReservedStock - 1);

  res.json({ status: 'Reservation confirmed', itemId });
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const currentQuantity =
    (await getCurrentReservedStockById(itemId)) ?? product.stock;

  res.json({
    itemId: product.Id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity,
  });
});

app.get('/list_products', (req, res) => {
  const prducts = listProducts.map((product) => ({
    itemId: product.Id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  }));
  res.json(prducts);
});

app.listen(1245);
