import Link from 'next/link';
import React from 'react';
import { Flex } from '../flex/styled';
import { FooterContainer } from './styled';

export default function Footer() {
    return (
        <FooterContainer>
            <Flex width={'70%'} maxWidth={'1040px'} justifyContentBetween>
                <div></div>
                <div>
                    © 2020
                </div>
            </Flex>
        </FooterContainer>
    );
}
