//package hello;
package ricardo.sueiras.springbootdemo;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
public class HelloController {
    
    @RequestMapping("/")
    public String index() {
        String str = "<html><body><h1>EKS Spring Boot application</h1><br><p>Java Runtime version is " + System.getProperty("java.runtime.version") + " from "+ System.getProperty("java.vm.name") + " and my Java home is " + System.getProperty("java.home") + "</p><br>\n";
        str = str.concat("<p1>Operating System details: ").concat(System.getProperty("os.arch")).concat(" ").concat(System.getProperty("os.name")).concat(" ").concat(System.getProperty("os.version")).concat("</p><br>\n");
        str = str.concat("Hope you enjoy the talk!<br><h1>Updated Source code for demo - should be the same on x86 and arm</h1> </body></html>");
        return str;
    }
    
}
