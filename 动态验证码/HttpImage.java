package utils;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.util.Scanner;

import org.apache.http.HttpEntity;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
 
public class HttpImage {
	
	/**
	 * 发送请求，获取响应
	 * @param urlString 服务地址
	 * @param path 图片路径
	 * @return
	 * @throws IOException
	 */
	public static String doPost(String urlString, String pathImage) throws IOException {

		URL url = new URL(urlString);
		URLConnection connection = url.openConnection();
		connection.setDoOutput(true);
 
		//try里面拿到输出流
		try (BufferedOutputStream bos = new BufferedOutputStream(connection.getOutputStream())) {
			
			//java代码是在Windows上运行的，图片路径就是下面这个			
			InputStream is = new FileInputStream(pathImage);
			BufferedInputStream bis = new BufferedInputStream(is);
			
			byte[] buf= new byte[1024];
			int length = 0;
			length = bis.read(buf);
			while(length!=-1) {
				bos.write(buf, 0, length);
				length = bis.read(buf);
			}
			bis.close();
			is.close();
			bos.close();
		}
	
		//如果有返回值，则返回数据
		StringBuilder response = new StringBuilder();
		try (Scanner in = new Scanner(connection.getInputStream())) {
			while (in.hasNextLine()) {
				response.append(in.nextLine());
				response.append("\n");
			}
		} catch (IOException e) {
			if (!(connection instanceof HttpURLConnection))
				throw e;
			InputStream err = ((HttpURLConnection) connection).getErrorStream();
			if (err == null)
				throw e;
			Scanner in = new Scanner(err);
			response.append(in.nextLine());
			response.append("\n");
			in.close();
		}
 
		return response.toString();
	}
	
	/**
	 * 下载验证码图片
	 * @param imageUrl 验证码图片链接
	 * @param savePath 验证码图片保存地址
	 * @throws ClientProtocolException
	 * @throws IOException
	 */
	 public static void downImage(String imageUrl, String savePath) throws ClientProtocolException, IOException   
	    {   
		 	CloseableHttpClient httpclient = HttpClients.createDefault();  
	        try { 
	            HttpGet httpGet = new HttpGet(imageUrl); 
	            CloseableHttpResponse response = httpclient.execute(httpGet); 
	            try { 
	                HttpEntity entity = response.getEntity(); 
	                InputStream inStream = entity.getContent(); 
	                FileOutputStream fw = new FileOutputStream(savePath, false); 
	    			int b = inStream.read(); 
	    			while (b != -1) { 
	    				fw.write(b); 
	    				b = inStream.read(); 
	    			} 
	                fw.close(); 
	                EntityUtils.consume(entity); 
	            } finally { 
	                response.close(); 
	            } 
	        }finally { 
	            httpclient.close(); 
	        } 
	    }  
	
	/**
	 * 获取图片验证码
	 * @param url  服务地址
	 * @param path  验证码图片路径
	 * @return String code 验证码
	 * @throws IOException
	 */
	public static String getCode(String serviceUrl, String imagePath) throws IOException {
		String result = HttpImage.doPost(serviceUrl, imagePath);
		JSONObject object = JSON.parseObject(result);
		String code = object.getString("code");
		return code;
	}
	
	public static void main(String[] args) throws IOException {
		
		
		String imageUrl = "https://www.95303.com/api/User/Send_tel_identifying?&type=2";
		String serviceUrl = "http://localhost:7788";	
		String pathImage = System.getProperty("user.dir") + "/src/main/java/utils/22.png";
		
		HttpImage.downImage(imageUrl, pathImage);  // 下载图片
		
		String code = HttpImage.getCode(serviceUrl, pathImage);  // 获取验证码
		
		System.out.println(code);
	}
 
}
