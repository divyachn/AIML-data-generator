# AIML-data-generator
### DATA ORGANISATION

'## intent:ABCD' versus '## pattern:XYZ' versus '## topic:EFGH'

'intent' is used when we take more than one variation of a given statement. For eg:
```
## intent:hello  
- hi  
- hii  
- Howdy.  
- Hey!  
```
'- hi', anything following '-' is an instance of what a user can write.  

'pattern' is used when a single instance of any type is taken. It won't have lines beginning with '-'. For eg:  
```
## pattern:It is very [*](today)  
$ Do you like it?  
;
```
`[*]`(today), it is something similar to Markdown format. It implies that create a variable today and assign it whatever is captured by the *.
	
Now coming to the Bot's response, it is anything following '$'.  
Understanding it with a small example:  
User: Howdy  
Bot: Hey.
- - -
User: Hello  
Bot: Hi user_name.

	<category>
	<pattern>HOWDY</pattern>
	<template><srai>HELLO</srai></template>
	</category>
	
	<category>
	<pattern>HELLO</pattern>
	<template>
	<random>
	<li>Hey.</li>
	<li>Hi user_name.</li>
	</random>
	</template>
	</category>
	
Translating the above, we get:
```
## intent:hello  
- Howdy  
$ Hey.  
$ Hi user_name.  
;
```
**Don't forget to put the ';' at the end.** It marks the ending of one unit of knowledge of bot.

Coming to the two types of usage of \<random> and how they are going to be translated?

#### Type I: Seperate \<random> within \<template>

Sentence I = ['Hello', 'Hi there', 'Howdy']  
Sentence II = ['How are you?', 'What's up?']

We can randomly select one entry from Sentence I and other from Sentence II and then join them to form one response.  
So we can have 'Hello How are you?' or 'Howdy What's up?'.

In AIML, it will look like:
```
	<template>
	<random>
	<li>Hello</li>
	<li>Hi there</li>
	<li>Howdy</li>
	</random>
	<random>
	<li>How are you?</li>
	<li>What's up?</li>
	</random>
	</template>
```
```
$ ['Hello', 'Hi there', 'Howdy']['How are you?', 'What's up?']
```
#### Type II: Nested \<random>

We can also have \<random> inside another \<random>. In AIML it will look like:  
```
<random>
<li>ABCD</li>
<li>good<random>
<li>XYZ</li>
<li>xyz</li>
</random>
</li>
<li>1234</li>
</random>
```

And it's translation:    
```
$ ABCD  
$ ['good']['XYZ', 'xyz']  
$ 1234
```
So far we saw how \<category>,\<pattern>,\<template>,\<random>,\<srai> are being implemented. Now we may have to keep context during the conversation. So, we need to use \<that>. Understanding it first with a sample conversation:

User: It is very xyz today.  
Bot: Do you like it?  
User: Yes.  
Bot: You are enjoying. That's good.  
- - -
User: It is very abcd today.  
Bot: Do you like it?  
User: No.  
Bot: That's sad. I don't know what to say.

One thing which can be observed is that 'yes', 'no' are very generic responses. The bot should know the question asked for which these replies are being given by user. So, we will use \<that>. One thing to remember is that \<that> tag remembers bot's last response not that of user.

	<category>
	<pattern>IT IS VERY * TODAY</pattern>
	<template>Do you like it?</template>
	</category>
	
	<category>
	<pattern>YES</pattern>
	<that>DO YOU LIKE IT</that>
	<template>You are enjoying. That's good.</template>
	</category>
	
	<category>
	<pattern>NO</pattern>
	<that>DO YOU LIKE IT</that>
	<template>That's sad. I don't know what to say.</template>
	</category>
```	
## pattern:it is very * today.  
$ Do you like it?  
	## pattern:yes  
	$ You are enjoying. That's good.  
	;
	## pattern:no  
	$ That's sad. I don't know what to say.  
	;  
;
```
Now what if the user would have said 'It is very hot today.' or 'It is very cold today.'. Then bot's response should depend on what value is being stored by *. Basically we need if-else/switch thing. Eg:

User: It is very hot today.  
Bot: Oh yes. This weather. I think I am going to melt.
- - -
User: It is very dry today.  
Bot: Yeah. My skin needs some moisturizer.

	<category>
	<pattern>IT IS VERY * TODAY</pattern>
	<template>
	<think><set name="today"><star/></set></think>
	<condition name="today">
	<li value="hot">Oh yes. This weather. I think I am going to melt.</li>
	<li value="dry">Yeah. My skin needs some moisturizer.</li>
	<li>Do you like it?</li>
	</condition>
	</template>
	</category>
	
We need to first assign * to the variable 'today'. That is done using \<set>. \<think> is used because it is not going to be visible to the user. More details about \<set> are given later. Once the value of 'today' is set, we use \<condition>. It's more like switch. But you need to write the default case, if any, only in the end. Depending on the value the response is made.
```
## pattern:it is very `[*]`(today) today.
$ ?today:
	case 'hot':
		$ Oh yes. This weather. I think I am going to melt.
		$ Yeah it's very hot.
	case 'dry':
		$ Yeah. My skin needs some moisturizer.
	default:
		$ Do you like it?
		$ Are you enjoying it?
	?
;
```
Setting of variables can be done in two ways, one using <think> and other without using it.

Case 1: Without \<think>:

	<category>
	<pattern>I am *</pattern>
	<template>Hello <set name="username"><star/></set>!</template>
	</category>

	<category>
	<pattern>Good Night</pattern>
	<template>Hi <get name="username"/>. Thanks for the conversation!</template>
	</category>
```
## pattern:I am *
$ Hello [<star/>](user_name)!
;
## pattern:good night
$ Hi {"user_name"}. Thanks for the conversation!
;
```
Case 2: Using \<think>

	<category>
	<pattern>My name is *</pattern>
	<template>Hello!
	<think><set name="username"><star/></set></think>
	</template>
	</category>

	<category>
	<pattern>Bye</pattern>
	<template>Hi <get name="username"/>. Thanks for the conversation!</template>
	</category>
```
## pattern:My name is [<star/>](user_name)
$ Hello
;
## pattern:Bye
$ Hi {user_name}. Thanks for the conversation!
;
```
**Case 3: Botmaster's will**  
There is one more case, when the botmaster will like to set some variables, then we will use a dictionary following the line beginning with '##', eg:
```
## intent:I am fine{'intent':'user_feel_fine', 'user_mood':'not_sad'}
- I am fine *
$ Good
;
```
Now coming to the \<topic>, ## topic:movies

User: Let's discuss movies.  
Bot: Yes.  
User: Do you watch movies.  
Bot: Watching good movie refreshes our minds.  //This response is given when the user writes something which is not defined in any \<pattern>  
User: I like watching comedy!  
Bot: I like comedy movies too.

In AIML it will be translated as:

	<category>
	<pattern>LET US DISCUSS MOVIES</pattern>
	<template>Yes <set name="topic">movies</set></template>
	</category>
   
	<topic name="movies">
	<category>
	<pattern> * </pattern>
	<template>Watching good movie refreshes our minds.</template>
	</category>
      
	<category>
	<pattern>I LIKE WATCHING COMEDY</pattern>
	<template>I like comedy movies too.</template>
	</category>
	</topic>
```	
## pattern:Let's discuss [movies](topic)
$ Yes
;
## topic:movies
## pattern:I like watching comedy
$ I like comedy movies too.
;
## pattern:*
$ Watching good movie refreshes our minds.
;
## topic:end_topic
;
