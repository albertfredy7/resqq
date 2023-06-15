import 'dart:convert';
import 'package:shelf/shelf.dart' as shelf;
import 'package:shelf/shelf_io.dart' as io;
import 'package:shelf_router/shelf_router.dart' as shelf_router;
import 'package:shelf_static/shelf_static.dart' as shelf_static;

void main() async {
  final app = shelf_router.Router();

  app.post('/receive-data', (shelf.Request request) async {
    final payload = await request.readAsString();
    final data = jsonDecode(payload) as Map<String, dynamic>;

    // Process the received location data
    final latitude = data['latitude'];
    final longitude = data['longitude'];

    // Do something with the location data
    print('Received location: Latitude $latitude, Longitude $longitude');

    return shelf.Response.ok('Location received successfully');
  });

  app.all('/<ignored|.*>',
      shelf_static.createStaticHandler('web', defaultDocument: 'index.html'));

  final server = await io.serve(app, 'localhost', 8000);
  print('Server running on localhost:${server.port}');
}
