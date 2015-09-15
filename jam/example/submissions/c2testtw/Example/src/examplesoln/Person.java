package examplesoln;


/**
 * A representation of an Person
 * Stores a name and an age.
 * @author Alexander Brown
 *
 */
public class Person {

    /**
     * The Person's name.
     */
    private String name;

    /**
     * The Person's age.
     */
    private int age;

    /**
     * Constructs a new Person with a name and an age.
     * @param name the name of the Person.
     * @param age the age of the Person.
     */
    public Person(String name, int age){
        this.name = name;
        this.age = age;
    }

    /**
     * Returns the Person's name.
     * @return the Person's name.
     */
    public String getName(){
        return this.name;
    }

    /**
     * Set this Person's name to name.
     * @param name the new name of the Person.
     */
    public void setName(String name){
        this.name = "I am " + name;
    }

    /**
     * Returns the Person's age.
     * @return the Person's age.
     */
    public int getAge(){
        return this.age;
    }

    /**
     * Set this Person's age to age.
     * @param age the new age of the Person.
     */
    public void setAge(int age){
        this.age = age;
    }

    public String toString(){
        return this.name + " is " + this.age + " years old.";
    }
}
