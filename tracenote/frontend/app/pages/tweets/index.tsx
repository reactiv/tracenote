import {
  VStack,
  Box,
  Spacer,
  Flex,
  Container,
  Button,
  ButtonGroup,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  IconButton,
  HStack,
  Input,
  InputGroup,
  InputRightElement
} from "@chakra-ui/react";
import React, {useState, useEffect} from "react";
import {GetServerSideProps} from "next";
import useSWR from 'swr'
import { fetcher } from '../../utils/index.js'
import {AddIcon, ChevronLeftIcon, ChevronRightIcon, SearchIcon} from "@chakra-ui/icons";
import {useRouter} from "next/router";
var qs = require('qs');

type TwitterUser = {
  id: number;
  username: string;
}

type Tweet = {
  id: number;
  text: string;
  author: TwitterUser;
};

type TweetQueryParameters = {
  q?: string;
  skip?: number;
  limit?: number;
}

interface TweetPageProps {
  tweets: Tweet[];
}

function replaceQs(q: Object, params: TweetQueryParameters) {
  return qs.stringify(Object.assign(params, q));
}

export default function Tweets() {
  const router = useRouter();
  const params = router.query as TweetQueryParameters;
  const skip = params.skip !== undefined ? parseInt(String(params.skip)) : 0
  const nextPage = <IconButton
    aria-label='Add to friends' icon={<ChevronRightIcon />}
    onClick={() => router.push(`/tweets?${replaceQs({skip: skip + 100}, params)}`)}
  />;
  const prevPage = <IconButton
    aria-label='Add to friends' icon={<ChevronLeftIcon />}
    onClick={() => router.push(`/tweets?${replaceQs({skip: (skip - 100) < 0 ? 0 : skip - 100},
      params)}`)}
  />;
  const [searchTerm, setSearchTerm] = useState('');


  useEffect(() => {
    if (params.q !== undefined) {
      setSearchTerm(params.q);
    }
  }, [params.q]);

  const { data, error } = useSWR(`http://localhost:8001/twitter/tweets?${replaceQs({}, params)}`, fetcher)
  const countString = (!data) ? '' : (
    `${skip + 1} - ${((skip + 100) < data.total) ? String(skip + 100) + ' of ' + data.total : data.total}`
  );

  const tweetRows = (!data) ? (<></>) : (data.tweets.map((tweet: Tweet) => (
    <Tr>
      <Td></Td>
      <Td>{tweet.author.username}</Td>
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
        <Flex w='100%'>
          <HStack>
            <Box>
              <ButtonGroup size='sm' isAttached variant='outline'>
                { prevPage }
                { nextPage }
              </ButtonGroup>
            </Box>
            <Box>
              {countString}
            </Box>
          </HStack>
          <Spacer />
          <Box>
            <InputGroup size='md'>
              <Input
                pr='3rem'
                value={searchTerm}
                placeholder='Search term'
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <InputRightElement width='3rem'>
                <IconButton
                  aria-label='Search' icon={<SearchIcon />}
                  h='1.75rem' size='sm'
                  onClick={() => router.push(`/tweets?${replaceQs({q: searchTerm, skip: 0}, params)}`)}
                />
              </InputRightElement>
            </InputGroup>
          </Box>
        </Flex>
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