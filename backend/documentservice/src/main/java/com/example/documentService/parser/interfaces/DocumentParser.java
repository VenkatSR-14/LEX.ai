package com.example.documentService.parser.interfaces;
import java.io.InputStream;
public interface DocumentParser {
    String parse(InputStream inputStream) throws Exception;
}
