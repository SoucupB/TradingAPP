var unirest = require("unirest");

var req = unirest("GET", "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete");

req.query({
	"q": "tesla",
	"region": "US"
});

req.headers({
	"x-rapidapi-key": "c92d41ade0msh5207d21a3bb27c3p1c233djsn8749b4aa51db",
	"x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com",
	"useQueryString": true
});


req.end(function (res) {
	if (res.error) throw new Error(res.error);

	console.log(res.body);
});
