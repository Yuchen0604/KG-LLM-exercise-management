## case 1

> NL version with no prerequisites
> theme: File Processing System

- KG competency: exceptions, try-catch blocks
```json
{
  "https://aet.cit.tum.de/tpo/example#Comp_TryCatch": {
    "title": "Try-Catch Blocks",
    "description": "Apply try-catch-finally blocks to handle exceptions gracefully and maintain program stability. Use appropriate exception handling strategies including catching specific exceptions, resource cleanup, and meaningful error recovery or reporting.",
    "taxonomy": [
      "Apply"
    ],
    "dependencies": [
      {
        "label": "Exceptions",
        "description": "Explain Java's exception mechanism including the distinction between checked and unchecked exceptions. Understand how exceptions represent error conditions, propagate through the call stack, and differ from normal return values.",
        "taxonomy": [
          "Understand"
        ],
        "relations": [
          "requires"
        ],
        "sub_dependencies": [
          {
            "label": "Inheritance",
            "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
            "taxonomy": [
              "Apply"
            ],
            "relations": [
              "requires"
            ]
          }
        ]
      },
      {
        "label": "Inheritance",
        "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
        "taxonomy": [
          "Apply"
        ],
        "relations": [
          "requires"
        ],
        "sub_dependencies": [
          {
            "label": "Class Definition",
            "description": "Design and create complete class definitions that model real-world entities or abstract concepts. Produce well-structured classes with appropriate fields, methods, and constructors that exhibit high cohesion and clear responsibility.",
            "taxonomy": [
              "Create"
            ],
            "relations": [
              "extends"
            ]
          },
          {
            "label": "Objects and Classes",
            "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "extends"
            ]
          }
        ]
      }
    ]
  },
  "https://aet.cit.tum.de/tpo/example#Comp_Exceptions": {
    "title": "Exceptions",
    "description": "Explain Java's exception mechanism including the distinction between checked and unchecked exceptions. Understand how exceptions represent error conditions, propagate through the call stack, and differ from normal return values.",
    "taxonomy": [
      "Understand"
    ],
    "dependencies": [
      {
        "label": "Inheritance",
        "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
        "taxonomy": [
          "Apply"
        ],
        "relations": [
          "requires"
        ],
        "sub_dependencies": [
          {
            "label": "Class Definition",
            "description": "Design and create complete class definitions that model real-world entities or abstract concepts. Produce well-structured classes with appropriate fields, methods, and constructors that exhibit high cohesion and clear responsibility.",
            "taxonomy": [
              "Create"
            ],
            "relations": [
              "extends"
            ]
          },
          {
            "label": "Objects and Classes",
            "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "extends"
            ]
          }
        ]
      }
    ]
  }
}
```
- NL: 
```
The exercise should focus on the following competencies:

Try-Catch Blocks
Apply try-catch-finally blocks to handle exceptions gracefully and maintain program stability. Use appropriate exception handling strategies including catching specific exceptions, resource cleanup, and meaningful error recovery or reporting.
    
Exceptions: 
Explain Java's exception mechanism including the distinction between checked and unchecked exceptions. Understand how exceptions represent error conditions, propagate through the call stack, and differ from normal return values.
    
The following prerequisite knowledge is required: 

```


## case 2

> NL version with incomplete prerequisites ?
> theme: user management system

- KG competency: object reference, null reference, object equality
```json
{
  "https://aet.cit.tum.de/tpo/example#Comp_NullReferences": {
    "title": "Null References",
    "description": "Explain the meaning of null as a reference that points to no object, and understand how NullPointerException occurs. Recognize situations where null values may arise and the importance of null checking in defensive programming.",
    "taxonomy": [
      "Understand"
    ],
    "dependencies": [
      {
        "label": "Object References",
        "description": "Explain how variables hold references to objects rather than objects themselves, and how multiple references can point to the same object. Understand the implications for parameter passing, assignment, and object sharing.",
        "taxonomy": [
          "Understand"
        ],
        "relations": [
          "requires"
        ],
        "sub_dependencies": [
          {
            "label": "Object Creation",
            "description": "Instantiate objects using constructors with the 'new' keyword, providing appropriate arguments to initialize object state. Apply object creation to build programs that utilize multiple interacting objects.",
            "taxonomy": [
              "Apply"
            ],
            "relations": [
              "extends"
            ]
          }
        ]
      }
    ]
  },
  "https://aet.cit.tum.de/tpo/example#Comp_References": {
    "title": "Object References",
    "description": "Explain how variables hold references to objects rather than objects themselves, and how multiple references can point to the same object. Understand the implications for parameter passing, assignment, and object sharing.",
    "taxonomy": [
      "Understand"
    ],
    "dependencies": [
      {
        "label": "Object Creation",
        "description": "Instantiate objects using constructors with the 'new' keyword, providing appropriate arguments to initialize object state. Apply object creation to build programs that utilize multiple interacting objects.",
        "taxonomy": [
          "Apply"
        ],
        "relations": [
          "extends"
        ],
        "sub_dependencies": [
          {
            "label": "Objects and Classes",
            "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "requires"
            ]
          }
        ]
      }
    ]
  },
  "https://aet.cit.tum.de/tpo/example#Comp_ObjectEquality": {
    "title": "Object Equality",
    "description": "Apply the distinction between reference equality (==) and object equality (equals method) when comparing objects. Use appropriate equality comparisons based on whether identity or logical equivalence is required.",
    "taxonomy": [
      "Apply"
    ],
    "dependencies": [
      {
        "label": "Object Creation",
        "description": "Instantiate objects using constructors with the 'new' keyword, providing appropriate arguments to initialize object state. Apply object creation to build programs that utilize multiple interacting objects.",
        "taxonomy": [
          "Apply"
        ],
        "relations": [
          "extends"
        ],
        "sub_dependencies": [
          {
            "label": "Objects and Classes",
            "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "requires"
            ]
          }
        ]
      },
      {
        "label": "Object References",
        "description": "Explain how variables hold references to objects rather than objects themselves, and how multiple references can point to the same object. Understand the implications for parameter passing, assignment, and object sharing.",
        "taxonomy": [
          "Understand"
        ],
        "relations": [
          "extends"
        ],
        "sub_dependencies": [
          {
            "label": "Object Creation",
            "description": "Instantiate objects using constructors with the 'new' keyword, providing appropriate arguments to initialize object state. Apply object creation to build programs that utilize multiple interacting objects.",
            "taxonomy": [
              "Apply"
            ],
            "relations": [
              "extends"
            ]
          }
        ]
      }
    ]
  }
}
```
- NL: 
```
The exercise should focus on the following competencies:

Object References:
Explain how variables hold references to objects rather than objects themselves, and how multiple references can point to the same object. Understand the implications for parameter passing, assignment, and object sharing.

Null References:
Explain the meaning of null as a reference that points to no object, and understand how NullPointerException occurs. Recognize situations where null values may arise and the importance of null checking in defensive programming.

Object Equality:
Understand how object equality is evaluated in Java, including the difference between reference equality (==) and logical equality using equals(). Recognize common pitfalls when comparing objects and implement meaningful equality checks where appropriate.

The following prerequisite knowledge is required:

Object Creation:
Instantiate objects using constructors with the 'new' keyword, providing appropriate arguments to initialize object state. Apply object creation to build programs that utilize multiple interacting objects.
```


## case 3

> NL version with complete 1 degree prerequisites


- KG competency: dynamic binding, inheritance
```
{
  "https://aet.cit.tum.de/tpo/example#Comp_DynamicBinding": {
    "title": "Dynamic Binding",
    "description": "Analyze how method calls are resolved at runtime based on the actual object type rather than the declared variable type. Trace polymorphic method invocations through class hierarchies to predict program behavior.",
    "taxonomy": [
      "Analyze"
    ],
    "dependencies": [
      {
        "label": "Inheritance",
        "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
        "taxonomy": [
          "Apply"
        ],
        "relations": [
          "requires"
        ],
        "sub_dependencies": [
          {
            "label": "Class Definition",
            "description": "Design and create complete class definitions that model real-world entities or abstract concepts. Produce well-structured classes with appropriate fields, methods, and constructors that exhibit high cohesion and clear responsibility.",
            "taxonomy": [
              "Create"
            ],
            "relations": [
              "extends"
            ]
          },
          {
            "label": "Objects and Classes",
            "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "extends"
            ]
          }
        ]
      },
      {
        "label": "Method Overriding",
        "description": "Apply method overriding to provide specialized implementations of inherited methods in subclasses. Use the @Override annotation, call superclass methods appropriately, and maintain the method contract while customizing behavior.",
        "taxonomy": [
          "Apply"
        ],
        "relations": [
          "requires"
        ],
        "sub_dependencies": [
          {
            "label": "Inheritance",
            "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
            "taxonomy": [
              "Apply"
            ],
            "relations": [
              "requires"
            ]
          }
        ]
      },
      {
        "label": "Polymorphism",
        "description": "Explain how polymorphism allows objects of different classes to be treated uniformly through a common supertype. Understand how polymorphism enables flexible, extensible code where new types can be added without modifying existing code.",
        "taxonomy": [
          "Understand"
        ],
        "relations": [
          "extends"
        ],
        "sub_dependencies": [
          {
            "label": "Inheritance",
            "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
            "taxonomy": [
              "Apply"
            ],
            "relations": [
              "requires"
            ]
          },
          {
            "label": "Static vs Dynamic Types",
            "description": "Explain the distinction between a variable's declared (static) type and the actual runtime (dynamic) type of the object it references. Understand how Java's type system uses compile-time type checking while supporting runtime polymorphism.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "requires"
            ]
          }
        ]
      }
    ]
  },
  "https://aet.cit.tum.de/tpo/example#Comp_Inheritance": {
    "title": "Inheritance",
    "description": "Apply inheritance to create subclass relationships using the 'extends' keyword, reusing and extending superclass functionality. Use inheritance to model is-a relationships and establish class hierarchies that reduce code duplication.",
    "taxonomy": [
      "Apply"
    ],
    "dependencies": [
      {
        "label": "Class Definition",
        "description": "Design and create complete class definitions that model real-world entities or abstract concepts. Produce well-structured classes with appropriate fields, methods, and constructors that exhibit high cohesion and clear responsibility.",
        "taxonomy": [
          "Create"
        ],
        "relations": [
          "extends"
        ],
        "sub_dependencies": [
          {
            "label": "Objects and Classes",
            "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
            "taxonomy": [
              "Understand"
            ],
            "relations": [
              "extends"
            ]
          }
        ]
      },
      {
        "label": "Objects and Classes",
        "description": "Explain the relationship between classes and objects, describing how a class serves as a blueprint that defines state (fields) and behavior (methods), while objects are individual instances created from that blueprint.",
        "taxonomy": [
          "Understand"
        ],
        "relations": [
          "extends"
        ],
        "sub_dependencies": []
      }
    ]
  }
}
```
- NL: 
```
The exercise should focus on the following competencies:

Dynamic Binding:
Analyze how method calls are resolved at runtime depending on the actual object type rather than the declared type. This involves understanding how polymorphic method calls behave in class hierarchies.

Inheritance:
Apply inheritance using the 'extends' keyword to build class hierarchies and reuse functionality.

The following prerequisite knowledge is required:

- Method Overriding: understanding how subclasses provide specialized implementations of inherited methods.
- Polymorphism: understanding how objects of different types can be treated uniformly via a common superclass.
- Class Definition: ability to design and implement classes with fields and methods.
```