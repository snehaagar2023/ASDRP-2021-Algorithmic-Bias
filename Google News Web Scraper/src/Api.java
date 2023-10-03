
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;


public class Api {

	public static void main(String[] args) throws Exception {
		URL url = new URL("https://api.thebipartisanpress.com/api/endpoints/beta/robert");
		URLConnection con = url.openConnection();
		HttpURLConnection http = (HttpURLConnection)con;
		http.setRequestMethod("POST"); // PUT is another valid option
		http.setDoOutput(true);
		
		String transcript = "WASHINGTON (AP) — President Donald Trump urged senior Justice Department officials to declare the results of the 2020 election “corrupt” in a December phone call, according to handwritten notes from one of the participants in the conversation.\r\n"
				+ "\r\n"
				+ "“Just say the election was corrupt and leave the rest to me and the R. Congressmen,” Trump said at one point to then-Acting Attorney General Jeffrey Rosen, according to notes taken by Richard Donoghue, who was then Rosen’s deputy and who was also on the call.\r\n"
				+ "\r\n"
				+ "The notes of the Dec. 27 call, released Friday by the House Oversight Committee, underscore the lengths to which Trump went to try to overturn the results of the election and to elicit the support of senior government officials in that effort. Emails released last month show Trump and his allies in the last weeks of his presidency pressured the Justice Department to investigate unsubstantiated claims of widespread election fraud, forwarding them conspiracy theories and even a draft legal brief they hoped would be filed with the Supreme Court.\r\n"
				+ "\r\n"
				+ "The pressure is all the more notable because just weeks earlier, Trump’s own attorney general William Barr, revealed that the Justice Department had found no evidence of widespread fraud that could have overturned the results. Unsubstantiated claims of fraud have been repeatedly rejected by judge after judge, including by Trump appointees, and by election officials across the country.\r\n"
				+ "\r\n"
				+ "“These handwritten notes show that President Trump directly instructed our nation’s top law enforcement agency to take steps to overturn a free and fair election in the final days of his presidency,” committee chairman Rep. Carolyn Maloney, a New York Democrat, said in a statement.\r\n"
				+ "\r\n"
				+ "She said the committee had begun scheduling interviews with witnesses as part of its investigation into Trump’s effort to overturn the results. The Justice Department earlier this week authorized six witnesses, including Rosen and Donoghue, to appear before the panel and provide “unrestricted testimony,” citing the public interest in the “extraordinary events” of those final weeks.\r\n"
				+ "\r\n"
				+ "The Dec. 27 call took place just days after Barr had resigned, leaving Rosen in charge of the department during a turbulent final weeks of the administration that also included the Jan. 6 riot at the U.S. Capitol in which pro-Trump loyalists stormed the building as Congress was gathered to certify the election results.\r\n"
				+ "\r\n"
				+ "During the call, according to the notes, Trump complained that people were “angry” and blaming the Justice Department for “inaction” and said that “We have an obligation to tell people that this was an illegal, corrupt election.” He claimed the department had failed to respond to legitimate complaints and reports of election-related crime.\r\n"
				+ "\r\n"
				+ "The Justice Department officials told Trump that the department had been investigating, including through hundreds of interviews, but that the allegations were not supported by evidence. They said that much of the information the president was getting was “false,” according to Donoghue’s notes.\r\n"
				+ "\r\n"
				+ "At one point in the conversation, the notes show, Rosen told Trump that the Justice Department “can’t + won’t snap its fingers + change the outcome of the election, doesn’t work that way.”\r\n"
				+ "\r\n"
				+ "Trump responded by saying: “Don’t expect you to do that, just say that the election was corrupt + leave the rest to me and the R. Congressmen,” according to the notes.\r\n"
				+ "\r\n"
				+ "Trump mused during the call about replacing Justice Department leadership with Jeffrey Clark, the then-assistant attorney general of the Environment and Natural Resources Division who also served as the acting head of the Civil Division. Donoghue replied that such a move would not change the department’s position.\r\n"
				+ "\r\n"
				+ "After The New York Times reported that Trump had been contemplating a plan to replace Rosen with Clark, the inspector general announced that it would investigate whether any former or current department officials “engaged in an improper attempt” to overturn the results of the presidential election.";
		
		byte[] out = ("{\"API\":\"gAAAAABeVpQJKRM5BqPX91XW2AKfz8pJosk182maAweJcm5ORAkkBFj__d2feG4H5KIeOKFyhUVSY_uGImiaSBCwy2L6nWxx4g==\",\"Text\":" + transcript + "}").getBytes(StandardCharsets.UTF_8);
		int length = out.length;

		http.setFixedLengthStreamingMode(length);
		http.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
		http.connect();
		try(OutputStream os = http.getOutputStream()) {
		    os.write(out);
		}
		try(BufferedReader br = new BufferedReader(
				  new InputStreamReader(con.getInputStream(), "utf-8"))) {
				    StringBuilder response = new StringBuilder();
				    String responseLine = null;
				    while ((responseLine = br.readLine()) != null) {
				        response.append(responseLine.trim());
				    }
				    System.out.println(response.toString());
				}

	}

}
