import redis from "redis";

const client = redis.createClient();

client.on("connect", () => console.log(`Redis client connected to the server`));

client.on("error", (err) =>
  console.log(`Redis client not connected to the server: ${err.message}`),
);

const values = {
  Portland: 50,
  Seattle: 80,
  "New York": 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

Object.entries(values).forEach((item) => {
  client.hset("HolbertonSchools", item[0], item[1], redis.print);
});
client.hgetall("HolbertonSchools", (_, replay) => console.log(replay));
