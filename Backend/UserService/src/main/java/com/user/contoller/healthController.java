package com.user.contoller;

import org.springframework.web.bind.annotation.RestController;

import java.sql.Connection;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;



@RestController
@RequestMapping("/health")
public class healthController {

    @Autowired
    private DataSource dataSource;
    
@GetMapping("/")
public ResponseEntity<?> getHealth() {
    try (Connection connection = dataSource.getConnection()){
        if(connection.isValid(1000)){
            return ResponseEntity.status(200).body("Connection successful");
        }
        else{
            return ResponseEntity.status(500).body("Connection unsuccessful");
        }
    }
    catch(Exception err){
        return ResponseEntity.badRequest().body("bad req");
    }
}

}
