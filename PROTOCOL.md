# Romi Control Protocol

NOTE ABOUT WEBSOCKETS


## Data Types
All data sent or received should be [Little Endian](https://en.wikipedia.org/wiki/Endianness).

| Name         	| Size (bytes) 	|
|--------------	|--------------	|
| Unsigned Int 	| 4            	|
| Float        	| 4            	|
| String       	| >4           	|

### Strings
Strings are encoded as an int representing the length followed 
by the character data.

## Server(Romi)bound

## Clientbound

### Value Update (Single)
This packet is designed to update a single data value on the client.

Note: This packet is not implemented by the web client, and it is never dispatched by the Romi.
TODO CONFIRM THIS IS NEVER SENT

<table>
<thead>
  <tr>
    <th>Packet ID</th>
    <th>Field Name</th>
    <th>Field Type</th>
    <th>Notes</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan=2>0x10</td>
    <td>Index</td>
    <td>Unsigned Int</td>
    <td>The index to update.</td>
  </tr>
  <tr>
    <td>Data</td>
    <td>Unsigned Int | Float</td>
    <td>The new data.</td>
  </tr>
</tbody>
</table>
