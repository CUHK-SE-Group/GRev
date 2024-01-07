package com.example.demo;

import org.opencypher.gremlin.translation.TranslationFacade;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

@RestController
public class GreetingController {
    static class Match {
        String match;
        int start;
        int end;

        Match(String match, int start, int end) {
            this.match = match;
            this.start = start;
            this.end = end;
        }
    }

    @PostMapping("/transform")
    public Greeting greeting(@RequestBody GreetingRequest request) {
        String name = request.getQuery();
        System.out.println(name);
        name = processString(name);
        String gremlin = transform(name);
        System.out.println(gremlin);
        return new Greeting(gremlin);
    }

    public static String transform(String cypherQuery) {
        TranslationFacade cfog = new TranslationFacade();
        return cfog.toGremlinGroovy(cypherQuery);
    }

    public static String processString(String s) {
        List<Match> matches = new ArrayList<>();
        Pattern pattern = Pattern.compile(":L\\d+");
        Matcher matcher = pattern.matcher(s);
        while (matcher.find()) {
            matches.add(new Match(matcher.group(), matcher.start(), matcher.end()));
        }

        if (matches.isEmpty()) {
            return s;
        }

        StringBuilder result = new StringBuilder(s.substring(0, matches.get(0).start) + matches.get(0).match);
        int prevEnd = matches.get(0).end;

        for (int i = 1; i < matches.size(); i++) {
            Match match = matches.get(i);
            if (s.substring(prevEnd, match.start).trim().equals("")) {
                prevEnd = match.end;
                continue;
            }
            result.append(s.substring(prevEnd, match.start)).append(match.match);
            prevEnd = match.end;
        }

        result.append(s.substring(prevEnd));
        return result.toString();
    }
}

class Greeting {
    private final String query;

    public Greeting(String message) {
        this.query = message;
    }

    public String getQuery() {
        return query;
    }
}
