package com.example.documentService.parser;


import com.example.documentService.parser.interfaces.DocumentParser;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Component;

import java.io.InputStream;

@Component
public class PDFParser implements DocumentParser {
    @Override
    public String parse(InputStream inputStream) throws Exception{
        try(PDDocument document = PDDocument.load(inputStream)){
            PDFTextStripper stripper = new PDFTextStripper();
            return stripper.getText(document);
        }
    }
}
