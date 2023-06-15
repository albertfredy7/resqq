import 'dart:convert';
import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart' as shelf_io;
import 'package:shelf_router/shelf_router.dart';

void main() async {
  final app = Router();

  String latitude = '';
  String longitude = '';

  app.post('/receive-data', (Request request) async {
    final requestBody = await request.readAsString();
    final requestData = jsonDecode(requestBody);
    latitude = requestData['latitude'].toString();
    longitude = requestData['longitude'].toString();
    print(
        'Received location from Streamlit: Latitude $latitude, Longitude $longitude');
    return Response.ok('Location received');
  });

  app.get('/location', (Request request) async {
    final data = {'latitude': latitude, 'longitude': longitude};
    final encodedData = jsonEncode(data);
    return Response.ok(encodedData,
        headers: {'content-type': 'application/json'});
  });

  final handler = const Pipeline().addMiddleware(logRequests()).addHandler(app);

  final server = await shelf_io.serve(handler, 'localhost', 8000);
  print('Server running on ${server.address.host}:${server.port}');
}
