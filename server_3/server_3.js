const WebSocket = require('ws');

let clientNumber = 0;
const clients = new Map();
var json_arr = [{ client: 1, type: 'run', x: 310, y: 480 }, { client: 2, type: 'run', x: 360, y: 480 }, { client: 3, type: "run", x: 460, y: 480 }]
var current_clients_counter = 0
class Client {
  constructor(socket) {
    clientNumber++;
    this.id = clientNumber;
    this.xCoord = 0;
    this.yCoord = 480;
    this.score = 0;
    this.socket = socket;
    this.state = 'run'// in good condition not crashed
    // Add any other properties you need for the client's state

    //this.sendData('Welcome to the WebSocket server');

  }

  sendData(data) {
    this.socket.send(data);
  }
}

const wss = new WebSocket.Server({ port: 8888 });

wss.on('connection', (ws) => {
  if (clientNumber >= 3) {
    return
  }
  console.log('Client connected');


  if (!clients.has(ws) && clientNumber < 3) {
    const client = new Client(ws);
    current_clients_counter += 1
    clients.set(ws, client);
  }

  ws.send("welcome to the server")
  //ws.send("ya rab men el server")
  //setInterval(function () { ws.send('Welcome to the WebSocket server TIMER') }, 1000);
  console.log("a client connected")
  ws.on('message', (message) => {
    decoded_message = message.toString()
    const client = clients.get(ws);
    //mesh beykhosh gowwa el tart ghaleban 3ayez buffer bardo yeb2a ana keda mastafadtesh haga bel websocket 3an el socket el 3adi
    if (decoded_message === 'run') {
      console.log('In the start condition');
      if (client.id === 1) {
        client.xCoord = 310;
        client.y_Coord = 480
        const coordinates = json_arr[0];
        console.log('sendong data now')
        const json = JSON.stringify(coordinates);

        // send the JSON data to the server
        client.sendData(json);
      } else if (client.id === 2) {
        client.xCoord = 360;
        client.y_Coord = 480
        console.log("sending for client 2")
        const coordinates = json_arr[1]
        const json = JSON.stringify(coordinates);

        client.sendData(json);
      } else if (client.id === 3) {
        client.xCoord = 460;
        client.y_Coord = 480
        const coordinates = json_arr[2];
        const json = JSON.stringify(coordinates);

        // send the JSON data to the server
        client.sendData(json);
        setTimeout(function () {
          console.log("One millisecond has passed.");
        }, 1); // wait for 1000 milliseconds (1 second)
        for (const [socket, client] of clients.entries()) {

          const starting_data = json_arr;
          const json = JSON.stringify(starting_data);

          // send the JSON data to the server
          console.log(`sending for CLIENT ${client.id}`)
          client.sendData(json);


        }
      }
    }
    else {
      if (decoded_message.length > 0) {
        console.log(`i am expecting a json and got ${decoded_message}`)
        json_arr[client.id - 1] = JSON.parse(message)
        console.log(`client.id: ${client.id}`)
        console.log(json_arr)
        for (const [socket, cliento] of clients.entries()) {
          const json_2 = JSON.stringify(json_arr[client.id - 1]);
          if (cliento.id != client.id) {
            cliento.sendData(json_2);
            console.log(`json_2 sent to cliento${cliento.id}`, json_2)
          }
        }
      }
    }
    console.log(`Received data from client ${client.id}:`, decoded_message);
    // Access and update the client's state as needed
    client.data = message;
  });

  ws.on('close', () => {
    const client = clients.get(ws);
    clients.delete(ws);
    current_clients_counter -= 1
    if (current_clients_counter <= 0) {
      clientNumber = 0;
      json_arr = [{ client: 1, type: 'run', x: 310, y: 480 }, { client: 2, type: 'run', x: 360, y: 480 }, { client: 3, type: "run", x: 460, y: 480 }]
    }
    console.log(`Client ${client.id} disconnected`);
  });

  ws.on('error', (err) => {
    const client = clients.get(ws);
    let errorMessage = '';
    if (err.message === 'read ECONNRESET') {
      errorMessage = `Client ${client.id} connection crashed`;
    }

    clients.delete(ws);
    current_clients_counter -= 1
    if (current_clients_counter <= 0) {
      clientNumber = 0;
      json_arr = [{ client: 1, type: 'run', x: 310, y: 480 }, { client: 2, type: 'run', x: 360, y: 480 }, { client: 3, type: "run", x: 460, y: 480 }]
    }

    console.error(`WebSocket error: ${errorMessage}`);
    ws.terminate(); // Close the WebSocket connection
  });
});

console.log('Server listening on port 8888');
