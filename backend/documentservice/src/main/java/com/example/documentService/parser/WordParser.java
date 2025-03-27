package com.example.documentService.parser;

import com.example.documentService.parser.interfaces.DocumentParser;
import org.apache.poi.xwpf.extractor.XWPFWordExtractor;
import org.apache.poi.xwpf.usermodel.XWPFDocument;

import java.io.InputStream;

public class WordParser implements DocumentParser {
    @Override
    public String parse(InputStream inputStream) throws Exception {
        try (XWPFDocument doc = new XWPFDocument(inputStream)){
            XWPFWordExtractor extractor = new XWPFWordExtractor(doc);
            return extractor.getText();
        }
    }
}
