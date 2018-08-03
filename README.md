# venmo_graph
After listening to Security Now! episode #673 which discusses Venmo's public transaction log. I thought it would be fun to look into. Given the nature of the data I wanted to create a large graph.
I wrote a quick python script to grab data from the api, used the data to create a graph(nodes being people and edges being transactions), and then export the data to a file in gefx(Graph Exchange XML format).

The problem I ran into was that venmo's api only allows 2 requests a minute each request containing about 20 transactions. This meant that gathering enough data to see any real connectivity in the graph would take too long.

Here is an image of the graph generated after a few queries to the api
![screenshot](img/Capture.png "an image of the graph")
