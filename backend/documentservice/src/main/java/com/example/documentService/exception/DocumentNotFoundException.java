package com.example.documentService.exception;

public class DocumentNotFoundException extends RuntimeException{
    public DocumentNotFoundException(String message){
        super(message);
    }
}
