package com.codex.hellospring.repository;

import com.codex.hellospring.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SpringDataJapMemberRepository
        extends
        JpaRepository<Member, Long>,
        MemberRepository {
    @Override
    Optional<Member> findByName(String name);
}
