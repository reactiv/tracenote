import {
  VStack,
  Flex, Container, Button, ButtonGroup, Heading, Table, Thead, Tbody, Tr, Th, Td
} from "@chakra-ui/react";
import React, {useState, useEffect} from "react";
import {GetServerSideProps} from "next";
import useSWR from 'swr'
import { fetcher } from '../../utils/index.js'

type Tweet = {
  id: number;
  text: string;
};

interface TweetPageProps {
  tweets: Tweet[];
}

export default function Tweets() {
  const { data, error } = useSWR('http://localhost:8001/twitter/tweets', fetcher)
  console.log(data)
  const tweetRows = (!data) ? (<></>) : (data.map((tweet: Tweet) => (
    <Tr>
      <Td></Td>
      <Td>Bob</Td>
      <Td dangerouslySetInnerHTML={{__html: tweet.text}} style={{whiteSpace: 'pre-line'}}/>
      <Td></Td>
    </Tr>
  )));
  return (
    <Container maxW="container.xl" p={0} my={40} h="100%" bg='gray.50'>
      <VStack
        w="full"
        h="full"
        p={10}
        spacing={10}
        alignItems="flex-start"
      >
        <Heading>Inbox</Heading>
        <Table>
          <Thead>
            <Tr>
              <Th/>
              <Th>
                Author
              </Th>
              <Th>
                Message
              </Th>
              <Th>
                Actions
              </Th>
            </Tr>
          </Thead>
          <Tbody>
            {tweetRows}
          </Tbody>
        </Table>
      </VStack>
    </Container>
  );
}