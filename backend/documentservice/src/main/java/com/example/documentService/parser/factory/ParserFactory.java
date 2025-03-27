package com.example.documentService.parser.factory;

import com.example.documentService.parser.PDFParser;
import com.example.documentService.parser.TextParser;
import com.example.documentService.parser.WordParser;
import com.example.documentService.parser.interfaces.DocumentParser;
import org.springframework.stereotype.Component;

@Component
public class ParserFactory {
    private final PDFParser pdfParser;
    private final WordParser wordParser;
    private final TextParser textParser;

    public ParserFactory(PDFParser pdfParser, WordParser wordParser, TextParser textParser){
        this.pdfParser = pdfParser;
        this.wordParser = wordParser;
        this.textParser = textParser;
    }
    public DocumentParser getParser(String fileType){
        if (fileType == null || fileType.isEmpty()){
            throw new IllegalArgumentException("File type cannot be null or empty");
        }
        switch (fileType.toLowerCase()){
            case "pdf":
                return new PDFParser();
            case "doc":
                return new WordParser();
            case "txt":
                return new TextParser();
            default:
                throw new IllegalArgumentException("Unsupported file type: " + fileType);
        }
    }
}
