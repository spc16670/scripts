import java.util.*;
import javax.mail.*;
import javax.mail.internet.*;
import javax.mail.internet.MimeMessage.RecipientType;
import javax.naming.*;
import javax.naming.directory.*;


public class Main {
	
	public static void main(String[] args) {
        try {
            String[] mx = getMX("gmail.com");
            for(String mxx : mx) {
                System.out.println("MX: " + mxx);
            }
            Properties props = new Properties();
            props.setProperty("mail.smtp.host", mx[0]);
            props.setProperty("mail.debug", "true");
            Session session = Session.getInstance(props);
            MimeMessage message = new MimeMessage(session);
            message.setFrom("szymonpiotrczaja@gmail.com");
            message.addRecipient(RecipientType.TO, new InternetAddress("szymonpiotrczaja@gmail.com"));
            message.setSubject("SMTP Test");
            message.setText("Hi Jan");
            Transport.send(message);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String[] getMX(String domainName) throws NamingException {
        Hashtable<String, Object> env = new Hashtable<String, Object>();

        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.dns.DnsContextFactory");
        env.put(Context.PROVIDER_URL, "dns:");

        DirContext ctx = new InitialDirContext(env);
        Attributes attribute = ctx.getAttributes(domainName, new String[] {"MX"});
        Attribute attributeMX = attribute.get("MX");
        // if there are no MX RRs then default to domainName (see: RFC 974)
        if (attributeMX == null) {
            return (new String[] {domainName});
        }

        // split MX RRs into Preference Values(pvhn[0]) and Host Names(pvhn[1])
        String[][] pvhn = new String[attributeMX.size()][2];
        for (int i = 0; i < attributeMX.size(); i++) {
            pvhn[i] = ("" + attributeMX.get(i)).split("\\s+");
        }

        // sort the MX RRs by RR value (lower is preferred)
        Arrays.sort(pvhn, (o1, o2) -> Integer.parseInt(o1[0]) - Integer.parseInt(o2[0]));

        String[] sortedHostNames = new String[pvhn.length];
        for (int i = 0; i < pvhn.length; i++) {
            sortedHostNames[i] = pvhn[i][1].endsWith(".") ? 
                pvhn[i][1].substring(0, pvhn[i][1].length() - 1) : pvhn[i][1];
        }
        return sortedHostNames;     
    }
	
}