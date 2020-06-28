let username = "Raeed";
let style = document.getElementById("username").innerHTML = username;

let xhr1 = new XMLHttpRequest;
xhr1.open('GET', "https://es64qwkzr1.execute-api.us-east-2.amazonaws.com/v4/bin?username=" + username, true);
xhr1.onload = function()
{
	if(this.status === 200)
	{
		var jsono = JSON.parse(this.responseText);
		console.log(jsono);
		for(var i in jsono)
		{
			console.log(jsono[i]);
			document.getElementById("orders").innerHTML = document.getElementById("orders").innerHTML + "<br><br>" + jsono[i].name;
			if(Boolean(jsono[i].instock))
			{
				document.getElementById("orders").innerHTML = "<br>" + document.getElementById("orders").innerHTML + " is in stock!";
			}
			else
			{
				document.getElementById("orders").innerHTML = "<br>" + document.getElementById("orders").innerHTML + " is out of stock!";
			}
		}
	}
}
xhr1.send();

document.getElementById("button").onclick = function()
{
	url = document.getElementById("url").value;
	let xhr2 = new XMLHttpRequest;
	xhr2.open('POST', "https://es64qwkzr1.execute-api.us-east-2.amazonaws.com/v4/bin?uname=" + username + "&url=" + encodeURI(url), true);
	xhr2.onload = function()
	{
		if(this.status === 200)
		{
			console.log(this.responseText);
		}
	}
	xhr2.send();
}

