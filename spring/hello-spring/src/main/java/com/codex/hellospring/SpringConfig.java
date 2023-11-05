package com.codex.hellospring;

import com.codex.hellospring.repository.MemberRepository;
import com.codex.hellospring.service.MemberService;
import jakarta.persistence.EntityManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class SpringConfig {

    private final DataSource datasource;
    private final EntityManager em;

    private final MemberRepository memberRepository;
    @Autowired
    public SpringConfig(DataSource datasource, EntityManager em, MemberRepository memberRepository) {
        this.datasource = datasource;
        this.em = em;
        this.memberRepository = memberRepository;
    }

    @Bean
    public MemberService memberService(){
        return new MemberService(memberRepository);
    }

//    @Bean
//    public MemberRepository memberRepository(){
//        //return new MemoryMemberRepository();
//        //return new JdbcMemberRepository(datasource);
//        //return new JdbcTemplateMemberRepository(datasource);
//        //return new JpaMemberRepository(em);
//        return memberRepository;
//    }
}
