package com.example.documentService.exception;

public class ParserException extends RuntimeException{
    public ParserException(String message, Throwable cause){
        super(message, cause);
    }
}
