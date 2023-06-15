import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String latitude = '';
  String longitude = '';

  @override
  void initState() {
    super.initState();
    fetchLocation();
  }

  Future<void> fetchLocation() async {
    final response =
        await http.get(Uri.parse('http://localhost:8000/location'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        latitude = data['latitude'].toString();
        longitude = data['longitude'].toString();
      });
      print('Latitude: $latitude');
      print('Longitude: $longitude');
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Server Demo',
      home: Scaffold(
        appBar: AppBar(
          title: Text('Location Data'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Latitude: $latitude',
                style: TextStyle(fontSize: 24),
              ),
              Text(
                'Longitude: $longitude',
                style: TextStyle(fontSize: 24),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
