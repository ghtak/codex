package com.codex.hellospring.service;

import com.codex.hellospring.domain.Member;
import com.codex.hellospring.repository.MemberRepository;
import com.codex.hellospring.repository.MemoryMemberRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MemberServiceTest {

    MemoryMemberRepository memberRepository = new MemoryMemberRepository();
    MemberService memberService = new MemberService(memberRepository);

    @AfterEach
    public void afterEach(){
        memberRepository.clearStore();
    }

    @Test
    void join() {
        //given
        Member member = new Member();
        member.setName("hello");

        //when
        Long saveId = memberService.join(member);

        //then
        Member findMember = memberService.findOne(saveId).get();
        Assertions.assertThat(member.getName()).isEqualTo(findMember.getName());
    }

    @Test
    public void duplicatedJoin(){
        Member member = new Member();
        member.setName("hello");

        Member new_member = new Member();
        new_member.setName("hello");

        memberService.join(member);
        IllegalStateException e = assertThrows(
                IllegalStateException.class,
                () -> memberService.join(new_member)
        );
        Assertions.assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다");
//        try {
//            memberService.join(new_member);
//            fail();
//        }catch (IllegalStateException ignored){
//
//        }
    }

    @Test
    void findMembers() {
    }

    @Test
    void findOne() {
    }
}