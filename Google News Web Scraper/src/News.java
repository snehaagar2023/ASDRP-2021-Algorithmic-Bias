import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

import org.jsoup.Connection.Response;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class News {
	
	public static String memory = "nothing";
	public static void main(String[] args) throws IOException {
		ArrayList<String> titles = new ArrayList<String>();
		ArrayList<String> links = new ArrayList<String>();
		ArrayList<Boolean> dates = new ArrayList<Boolean>();
		ArrayList<String> dates2 = new ArrayList<String>();
		Scanner input = new Scanner(System.in);
		System.out.println("Enter Date");
		String date = input.nextLine();
		System.out.println("Enter Number of Articles (From 2 to 100)");
		int NoA = input.nextInt();
		input.nextLine();
		System.out.println("Enter URL to scrape");
		String scrape = input.nextLine();
		
		Document doc = Jsoup.connect(scrape).get();
		String csv = "";
		String ohtml = doc.html();
//		System.out.println(ohtml);
		String[] s1 = ohtml.split("</a>");
		for(int i = 0; i < s1.length; i++) {
			String[] s2 = s1[i].split(">");
			if(s2[s2.length-1].contains("<a") || s2[s2.length-1].contains("</") || s2[s2.length-1].contains("img")) {
				
			}
			else {
				titles.add(s2[s2.length-1]);
			}

		}
		String[] s3 = ohtml.split("href=");
		for(int i = 0; i < s3.length; i++) {
			String[] s4 = s3[i].split("\"");
			if(s4[1].contains("./articles") && !s4[1].contentEquals(memory)) {
				links.add(s4[1]);
				memory = s4[1];
			}		

		}
		String[] s5 = ohtml.split("</time>");
		for(int i = 0; i < s5.length; i++) {
			String[] s6 = s5[i].split(">");
			if(s6[s6.length-1].contains("hour") || s6[s6.length-1].contains("Hour") || s6[s6.length-1].contains("minute") || s6[s6.length-1].contains("Minute")) {
				dates2.add(s6[s6.length-1]);
				dates.add(true);
			}
			else if(s6[s6.length-1].contains("day") || s6[s6.length-1].contains("Day")) {
				dates2.add(s6[s6.length-1]);
				dates.add(false);
			}

		}
		HashMap<String, String> biases = new HashMap<String, String>();
		biases.put("CNN", "Left");
		biases.put("Fox News", "Right");
		biases.put("Washington Post", "Left-Center");
		biases.put("New York Times", "Left-Center");
		biases.put("Wall Street Journal", "Right-Center");
		biases.put("New York Post", "Right-Center");
		biases.put("POLITICO", "Left-Center");
		biases.put("Business Insider", "Left-Center");
		biases.put("HuffPost", "Left");
		biases.put("Associated Press", "Neutral");
		biases.put("Reuters", "Neutral");
		biases.put("The Hill", "Neutral");
		biases.put("Los Angeles Times", "Left-Center");
		biases.put("CBS", "Left-Center");
		biases.put("CNBC", "Left-Center");
		biases.put("MSNBC", "Left");
		biases.put("BBC", "Left-Center");
		biases.put("Daily Mail", "Right");
		biases.put("NPR", "Left-Center");
		biases.put("USA TODAY", "Left-Center");
		biases.put("NBC News", "Left-Center");
		biases.put("Bloomberg", "Left-Center");
		biases.put("The Guardian", "Left-Center");
		HashMap<String, String> factuality = new HashMap<String, String>();
		factuality.put("CNN", "Mixed");
		int boost = 4;
		for(int i = 0; i < NoA; i++) {
			System.out.println("-------------------------------------------------");
			System.out.println("Article Number:" + (i+1));
			System.out.println(titles.get(2*i+boost));
			int acceptance = input.nextInt();
			input.nextLine();
			if(acceptance == 1) {
				System.out.println(titles.get(2*i+boost+1));
				String eval = null;
				boolean match = false;
				for(String s : biases.keySet()) {
					if(titles.get(2*i+5).contains(s)) {
						eval = biases.get(s);
						match = true;
					}
				}
				if(match) {
					System.out.println("match found");
				}
				else {
					eval = input.nextLine();
				}
				System.out.println("Article Age: " + dates2.get(i) + " - " + dates.get(i));
//				int proceed = input.nextInt();
//				if(proceed == 1) {
//					
//				}
//				else {
//					dates.set(i, !dates.get(i));
//					System.out.println("Changed to " + dates.get(i));
//				}
				csv += titles.get(2*i + boost);
				csv += "\t";
				String url = "https://news.google.com" + links.get(i).substring(1);
				Response response = Jsoup.connect(url).execute();
				csv +=  response.url();
				csv += "\t";
				csv += titles.get(2*i + boost+1);
				csv += "\t";
				csv += eval;
				csv += "\t";
				csv += (i+1);
				csv += "\t";
				csv += date;
				csv += "\t";
				csv += dates.get(i);
				csv += "\t";
				csv += "\n";
				
			}
			else {
				if(acceptance == 0) {
					boost+=1;
					i--;
				}
				else {
					titles.remove(2*i+boost+1);
					titles.remove(2*i+boost);
					links.remove(i);
					dates.remove(i);
					dates2.remove(i);
					i--;
				}
			}
		}
		FileWriter writer = new FileWriter("table.csv");
		writer.write(csv);
		writer.close();
	}

}
