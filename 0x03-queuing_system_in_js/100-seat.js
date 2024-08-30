import e from 'express';
import { createQueue } from 'kue';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
const asyncSet = promisify(client.set).bind(client);
const asyncGet = promisify(client.get).bind(client);

const queue = createQueue();

const app = e();

client.set('available_seats', 50);
let reservationEnabled = true;

async function reserveSeat(number) {
  await asyncSet('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await asyncGet('available_seats');
  return parseInt(seats);
}

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', async (req, res) => {
  if (reservationEnabled === false) {
    return res.json({ status: 'Reservation are blocked' });
  }
  const job = queue.create('reserve_seat', {});
  job.save((err) => {
    if (err) return res.json({ status: 'Reservation failed' });
    res.json({ status: 'Reservation in process' });
  });
  job.on('complete', () =>
    console.log(`Seat reservation job ${job.id} completed`),
  );
  job.on('failed', (err) =>
    console.log(`Seat reservation job ${job.id} failed: ${err}`),
  );
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const newAvailableSeats = (await getCurrentAvailableSeats()) - 1;
    await reserveSeat(newAvailableSeats);
    if (newAvailableSeats == 0) {
      reservationEnabled = false;
    }
    if (newAvailableSeats >= 0) done();
    else done(new Error('Not enough seats available'));
  });
  res.json({ status: 'Queue processing' });
});

app.listen(1245);
