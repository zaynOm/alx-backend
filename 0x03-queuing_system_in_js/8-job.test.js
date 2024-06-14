const { createQueue } = require('kue');
const createPushNotificationsJobs = require('./8-job');
const { expect } = require('chai');

const queue = createQueue();

describe('createPushNotificationsJobs', function () {
  before(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it("display an error message if jobs isn't an Array", function () {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(
      Error,
      'Jobs is not an array',
    );
  });

  it('create two new jobs to the queue', function () {
    const jobs = [
      { phoneNumber: '0807883425', message: 'hello' },
      { phoneNumber: '0807883425', message: 'hello' },
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
  });
});
