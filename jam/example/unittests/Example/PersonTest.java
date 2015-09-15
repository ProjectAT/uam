package Example;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import examplesoln.Person;
import edu.toronto.cs.jam.annotations.Description;

public class PersonTest {

    @Before
    public void setUp() throws Exception {
    }

    @After
    public void tearDown() throws Exception {
    }

    @Test(timeout=50)
    @Description(description="the Person constructor")
    public void testPerson() {
        // Test constructor
        new Person("John Smith", 40);
    }

    @Test(timeout=50)
    @Description(description="the getName() method")
    public void testGetName() {
        Person person = new Person("John Smith", 40);
        assertEquals("A Person's name should be set by input to the constructor\n", "John Smith", person.getName());
    }

    @Test(timeout=50)
    @Description(description="the getName() method")
    public void testGetNameEmpty(){
        Person person = new Person("", 40);
        assertEquals("An empty name should work\n", "", person.getName());
    }

    @Test(timeout=50)
    @Description(description="the getName() method")
    public void testGetFirstNameMultiplePeople() {
        Person firstPerson = new Person("John Smith", 40);
        Person secondPerson = new Person("Jane Smith", 36);
        Person thirdPerson = new Person("Simon Says", 10);
        assertEquals("name should not be static\n", "John Smith", firstPerson.getName());
        assertEquals("name should not be static\n", "Jane Smith", secondPerson.getName());
    }

    @Test(timeout=50)
    @Description(description="the getName() method")
    public void testGetNameAfterSetAge(){
        Person person = new Person("Jane Doe", 42);
        person.setAge(30);
        assertEquals("name should not be changed by setAge\n", "Jane Doe", person.getName());
    }

    @Test(timeout=50)
    @Description(description="the getAge() method")
    public void testGetAge() {
        Person person = new Person("Jane Smith", 30);
        assertEquals("A Person's age should be set by input to the constructor\n", 30, person.getAge());
    }

    @Test(timeout=50)
    @Description(description="the getAge() method")
    public void testGetAgeMultiplePeople() {
        Person firstPerson = new Person("John Doe", 56);
        Person secondPerson = new Person("Jane Smith", 36);
        Person thirdPerson = new Person("Simone Says", 14);
        assertEquals("age should not be static\n", 56, firstPerson.getAge());
        assertEquals("age should not be static\n", 36, secondPerson.getAge());
    }

    @Test(timeout=50)
    @Description(description="the getAge() method")
    public void testGetAgeAfterSetName() {
        Person person = new Person("Simon Says", 10);
        person.setName("Simone");
        assertEquals("age should not be changed by setName\n", 10, person.getAge());
    }

    @Test(timeout=50)
    @Description(description="the setName(String) method")
    public void testSetName(){
        Person person = new Person("John Smith", 40);
        person.setName("Jack Smith");
        assertEquals("name should be changed by setName\n", "Jack Smith", person.getName());
    }

    @Test(timeout=50)
    @Description(description="the setAge(int) method")
    public void testSetAge() {
        Person person = new Person("Simon Says", 10);
        person.setAge(5);
        assertEquals("age should be set to input of setAge\n", 5, person.getAge());
    }

    @Test(timeout=50)
    @Description(description="the toString() method")
    public void testToString() {
        Person person = new Person("John Smith", 40);
        assertEquals("John Smith is 40 years old.", person.toString());
    }

    @Test(timeout=50)
    @Description(description="the toString() method")
    public void testToStringAfterSet() {
        Person person = new Person("John Smith", 40);
        person.setName("Simone Says");
        person.setAge(14);
        assertEquals("The return value of toString should change with setter calls\n", "Simone Says is 14 years old.", person.toString());
    }

}
