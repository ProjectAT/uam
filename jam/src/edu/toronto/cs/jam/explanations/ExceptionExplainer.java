package edu.toronto.cs.jam.explanations;

import org.junit.runner.notification.Failure;

import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

import java.util.HashMap;

import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.events.XMLEvent;
import javax.xml.stream.events.StartElement;

/**
 * A class that contains logic for explaining the causes of different classes
 * of exceptions.
 *
 */
public final class ExceptionExplainer {

    public static final String COMPILE_ERROR_MSG = 
	"Compilation errors! Could not run any tests for this class.";

    /**
     * String constant for parsing XML for exception elements.
     */
    private static final String EXCEPTION = "exception";

    /**
     * String constant for parsing XML for the name of an exception.
     */
    private static final String NAME = "name";

    /**
     * String constant for parsing XML for the explanation for an exception.
     */
    private static final String EXPLANATION = "explanation";

    /**
     * HashMap for storing exception explanations.
     */
    private static HashMap<String, String> explanationMap =
            new HashMap<String, String>();

    /**
     * String constant for the default exception explanation.
     */
    private static final String DEFAULTEXPLANATION = null;

    /**
     * Private constructor.
     */
    private ExceptionExplainer() {
    }

    /**
     * Map exception names to explanation strings as in the given XML doument.
     * XML reading is done with a StAX API
     * @param path String path to exception explanation containing XML document
     */
    public static void updateExplanations(final String path) {
        String exceptionName = "";
        String exceptionExplanation = "";

        try {
            // Set up an XMLEventReader
            InputStream in = new FileInputStream(path);
            XMLInputFactory inputFactory = XMLInputFactory.newInstance();
            XMLEventReader eventReader = inputFactory.createXMLEventReader(in);

            // Parse the XML document
            while (eventReader.hasNext()) {
                XMLEvent event = eventReader.nextEvent();

                // If the current event is the start of an Exception, get the
                // name of the exception and set the corresponding explanation
                if (event.isStartElement()) {
                    StartElement startElement = event.asStartElement();

                    if (startElement.getName().getLocalPart()
                            .equals(EXCEPTION)) {
                        while (eventReader.hasNext()) {
                            event = eventReader.nextEvent();

                            if (event.isStartElement()) {
                                if (event.asStartElement().getName()
                                        .getLocalPart().equals(NAME)) {
                                    event = eventReader.nextEvent();
                                    exceptionName =
                                            event.asCharacters().getData();
                                    continue;
                                }

                                if (event.asStartElement().getName()
                                        .getLocalPart().equals(EXPLANATION)) {
                                    event = eventReader.nextEvent();
                                    exceptionExplanation =
                                            event.asCharacters().getData();
                                    continue;
                                }
                            }

                            if (event.isEndElement()) {
                                // At the end of an Exception, put the
                                // exceptionName and exceptionExplanation in the
                                // map as a key,value pair and break from the
                                // inner while loop
                                if (event.asEndElement().getName()
                                        .getLocalPart().equals(EXCEPTION)) {
                                    // If the exceptionExplanation is an empty
                                    // string, use null for the value of the
                                    // key,value pair.
                                    if (exceptionExplanation.isEmpty()) {
                                        explanationMap.put(exceptionName, null);
                                    } else {
                                        explanationMap.put(exceptionName,
                                                exceptionExplanation);
                                    }

                                    exceptionName = "";
                                    exceptionExplanation = "";
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (XMLStreamException e) {
            e.printStackTrace();
        }
    }
   
    /**
     * Consruct a message for this failure (to write to JSON).
     * @param failure Failure for which the message is built
     * @return A message for this failure (to write to JSON)
     */
    public static String failureMessage(final Failure failure) {
	return (failure.getMessage() == null) ? "" : failure.getMessage();
    }
}
