import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:frontend/apiUrls.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

class apiCaller{
  String serverIp; //Should have port //FIXME

  apiCaller({required this.serverIp});
  late final dio = Dio(BaseOptions(baseUrl: 'http://$serverIp',
  connectTimeout: const Duration(seconds: 30), //Set from env FIXME
  receiveTimeout: const Duration(seconds: 20) )
  );

  final _storage = const FlutterSecureStorage();
  late String _accessTokenKey = '$serverIp/accessToken';
  late String _refreshTokenKey = '$serverIp/refreshToken';

  Future<void> saveAccessToken(String token) async {
    await _storage.write(key: _accessTokenKey, value: token);
  }

  Future<void> saveRefreshToken(String token) async {
    await _storage.write(key: _refreshTokenKey, value: token);
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: _refreshTokenKey);
  }

  Future<void> deleteTokens() async {
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }

  void swapServers(String ip){
    serverIp = ip;
    dio.options.baseUrl = 'https://$serverIp/';
    _accessTokenKey = '$serverIp/accessToken';
    _refreshTokenKey = '$serverIp/refreshToken';
  }


  void intercept(){
    dio.interceptors.add(InterceptorsWrapper(
    onRequest: (options, handler) async {
      print("Request Interceptor");
      // Modify the request if needed
      var accessToken = await getAccessToken(); 
      if (accessToken != null){
        print("accessToken added");
        dio.options.headers["Authorization"] = 'Bearer $accessToken';
      }
      return handler.next(options); // continue
    },
    onError: (DioException e, handler) async {
      print(e.error);
      print(1);
        var accessToken = await getAccessToken();

      // Handle the error if needed
      if (e.response?.statusCode != 401){
        print(e.error);
        throw(e);
      }
      if ( accessToken ==null || JwtDecoder.isExpired(accessToken)  ){
        var refreshToken = await getRefreshToken();
        await dio.post(refreshTokenUrl, data: {"refresh": refreshToken}).then((Response e)=>{saveAccessToken(e.data["access"])});
        print("refreshed Tokens");
        return handler.resolve(await dio.fetch(e.requestOptions));
      }
      else{
        deleteTokens();
        print("log back in to $serverIp"); //Fixme logger // FIXME move back to login page
      }
      print(e.error);
      return handler.next(e);
    },
  ));

  }
  
  
  String catchDioException(DioException e){
      switch (e.type) {
      case DioExceptionType.connectionTimeout:
        print('connection timeout');
        return 'connection timeout';
      case DioExceptionType.sendTimeout:
        print('send timeout');
        return 'send timeout';
      case DioExceptionType.receiveTimeout:
        print('receive timeout');
        return 'receive timeout';
      case DioExceptionType.badCertificate:
        print('bad certificate');
        return 'bad certificate';
      case DioExceptionType.badResponse:
        print('bad response');
        return 'bad response';
      case DioExceptionType.cancel:
        print('request cancelled');
        return 'request cancelled';
      case DioExceptionType.connectionError:
        print('connection error');
        return 'connection error';
      case DioExceptionType.unknown:
        print(e.error);
        return 'unknown';
  }
  }

  
  Future<String> register(final username, final password) async {
    try {
      final response = await dio.post("$userRegister", data:{"username":username, "password":password});
      if (response.statusCode == 201){
      return "$username was created on server $serverIp.";
      }
      return "Successfully Created User: $username";
    } on DioException catch (e) {
      return catchDioException(e);
    }

    }
    

  Future<String> login(final username, final password) async {
    try {
      print("trying");
      final response = await dio.post("$loginUrl", data:{"username":username, "password":password});
      print("success");
      await saveAccessToken(response.data["access"]);
      await saveRefreshToken(response.data["refresh"]);
      intercept();
      return "$username was logged in.";
      
      return "Successfully logged on to $serverIp as $username";
    } on DioException catch (e) {
      return catchDioException(e);
    }
    }

  Future<String> getRun() async{
    final response = await dio.get('$getRunlist/2.json');
    return response.toString();
  }
    
}