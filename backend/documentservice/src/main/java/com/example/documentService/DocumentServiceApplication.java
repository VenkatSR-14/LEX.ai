package com.example.documentService;
import java.io.File;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;



@SpringBootApplication
public class DocumentServiceApplication {

	public static void main(String[] args) {
		File uploadDir = new File("uploads");
		if (!uploadDir.exists()){
			uploadDir.mkdirs();
		}
		SpringApplication.run(DocumentServiceApplication.class, args);
	}


}
