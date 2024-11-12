const app = require('fastify')();
const fs = require('fs');

app.register(require('@fastify/view'), {
  engine: {
    ejs: require('ejs'),
  },
});

const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

app.get('/', (req, res) => {
  const message = req.query.message;
  if (!message || typeof message !== 'string') {
    return res.redirect(`/?message=Yes%2C%20<b>we%20can<%2Fb>%21`);
  }
  const sanitized = DOMPurify.sanitize(message);
  res.view("/index.ejs", { sanitized: sanitized });
});

app.get('/design.css', (_, res) => {
  res.type('text/css').send(fs.readFileSync('design.css'));
});

app.listen({ port: process.env.PORT || 3000, host: '0.0.0.0' })
