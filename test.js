// we need axios to make HTTP requests
const axios = require('axios');

// and we need jsdom and Readability to parse the article HTML
const { JSDOM } = require('jsdom');
const { Readability } = require('@mozilla/readability');

// First lets get some search data from News API

// Build the URL we are going request. This will get articles related to green economy in English
let url = 'https://newsapi.org/v2/everything?' +
'q=green%20economy&' + // Search for green economy articles
'language=en&' + // Specify English language
'sortBy=publishedAt&' +
'apiKey=08e1a58d01f646b8aa2bf15e7e590ee0';

// Make the request with axios' get() function
axios.get(url).then(function(r1) {

  // At this point we will have some search results from the API. Take the first search result...
  let firstResult = r1.data.articles[1];

  // ...and download the HTML for it, again with axios
  axios.get(firstResult.url).then(function(r2) {

    // We now have the article HTML, but before we can use Readability to locate the article content we need jsdom to convert it into a DOM object
    let dom = new JSDOM(r2.data, {
      url: firstResult.url
    });

    // now pass the DOM document into readability to parse
    let article = new Readability(dom.window.document).parse();

    // Done! The article content is in the textContent property
    console.log(article.textContent);
  })
})